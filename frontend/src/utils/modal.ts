import NotImplementedModal from '@/components/common/NotImplementedModal.vue'

export function useNotImplementedModal() {
  const overlay = useOverlay()

  const modal = overlay.create(NotImplementedModal)

  return {
    showNotImplementedModal: (message?: string) => modal.open({ message }),
  }
}
