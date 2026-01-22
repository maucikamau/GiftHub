import type { ChatConversation, ChatConversationModel } from '@/types/chat.ts'
import { createSharedComposable } from '@vueuse/core'
import { ref } from 'vue'
import DonationRequestModal from '@/components/chat/requests/DonationRequestModal.vue'
import PaymentRequestModal from '@/components/chat/requests/PaymentRequestModal.vue'
import StripeConnectModal from '@/components/chat/requests/StripeConnectModal.vue'
import NotImplementedModal from '@/components/common/NotImplementedModal.vue'
import ConfirmDeliveryModal from '@/components/modals/ConfirmDeliveryModal.vue'
import DeleteConfirmationModal from '@/components/modals/DeleteConfirmationModal.vue'
import FeedbackModal from '@/components/modals/FeedbackModal.vue'
import { can } from '@/lib/permissions.ts'

function useModalInterface() {
  const overlay = useOverlay()

  const notImplemented = overlay.create(NotImplementedModal)
  const donationRequest = overlay.create(DonationRequestModal)
  const paymentRequest = overlay.create(PaymentRequestModal)
  const stripeConnect = overlay.create(StripeConnectModal)
  const confirmDelivery = overlay.create(ConfirmDeliveryModal)
  const feedback = overlay.create(FeedbackModal)
  const deleteConfirmation = overlay.create(DeleteConfirmationModal)

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
    showConfirmDeliveryModal: () => confirmDelivery.open({}),
    showFeedbackModal: (donorId: number, donorName: string) => feedback.open({ donorId, donorName }),
    showDeleteConfirmationModal: (itemName: string, itemType: 'listing' | 'campaign') =>
      deleteConfirmation.open({ itemName, itemType }),
  }
}

export const useModal = createSharedComposable(useModalInterface)
