import type { ChatConversation, ChatConversationModel } from '@/types/chat.ts'
import { createSharedComposable } from '@vueuse/core'
import { ref } from 'vue'
import DonationRequestModal from '@/components/chat/requests/DonationRequestModal.vue'
import PaymentRequestModal from '@/components/chat/requests/PaymentRequestModal.vue'
import StripeConnectModal from '@/components/chat/requests/StripeConnectModal.vue'
import NotImplementedModal from '@/components/common/NotImplementedModal.vue'
import { can } from '@/lib/permissions.ts'

function useModalInterface() {
  const overlay = useOverlay()

  const notImplemented = overlay.create(NotImplementedModal)
  const donationRequest = overlay.create(DonationRequestModal)
  const paymentRequest = overlay.create(PaymentRequestModal)
  const stripeConnect = overlay.create(StripeConnectModal)

  const pendingPaymentConversation = ref<ChatConversation | null>(null)

  async function showPaymentRequestDialog(forConversation: ChatConversation) {
    // If the user has no permission to view payments,
    // we need to connect with Stripe first.
    if (!can('payments.view_payment')) {
      // Store the conversation for later use
      pendingPaymentConversation.value = forConversation

      // Show Stripe connection modal first
      const res = await stripeConnect.open({ forConversation })
      if (res) {
        paymentRequest.open({ forConversation })
      }
      pendingPaymentConversation.value = null

      return
    }
    paymentRequest.open({ forConversation })
  }

  return {
    showNotImplementedModal: (message?: string) => notImplemented.open({ message }),
    showDonationRequestModal: (forConversation: ChatConversationModel) => donationRequest.open({ forConversation }),
    showPaymentRequestDialog,
    showStripeConnectModal: (forConversation: ChatConversation) => stripeConnect.open({ forConversation }),
  }
}

export const useModal = createSharedComposable(useModalInterface)
