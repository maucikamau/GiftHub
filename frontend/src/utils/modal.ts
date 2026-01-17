import type { ChatConversation, ChatConversationModel } from '@/types/chat.ts'
import { createSharedComposable } from '@vueuse/core'
import DonationRequestModal from '@/components/chat/requests/DonationRequestModal.vue'
import PaymentRequestModal from '@/components/chat/requests/PaymentRequestModal.vue'
import NotImplementedModal from '@/components/common/NotImplementedModal.vue'

function useModalInterface() {
  const overlay = useOverlay()

  const notImplemented = overlay.create(NotImplementedModal)
  const donationRequest = overlay.create(DonationRequestModal)
  const paymentRequest = overlay.create(PaymentRequestModal)

  return {
    showNotImplementedModal: (message?: string) => notImplemented.open({ message }),
    showDonationRequestModal: (forConversation: ChatConversationModel) => donationRequest.open({ forConversation }),
    showPaymentRequestDialog: (forConversation: ChatConversation) => paymentRequest.open({ forConversation }),
  }
}

export const useModal = createSharedComposable(useModalInterface)
