import type { ChatConversation } from '@/lib/streamChat.ts'
import { useInfiniteQuery } from '@tanstack/vue-query'
import { chatClient, isChatClientReady } from '@/lib/streamChat.ts'

export function useGetRecentConversations() {
  const PER_PAGE = 20
  return useInfiniteQuery({
    queryKey: ['conversations', 'recent'],
    initialPageParam: 0,
    getNextPageParam: (lastPage, _, lastPageParam) => {
      if (!lastPage) {
        return undefined
      }
      return lastPageParam + 1
    },
    getPreviousPageParam: (_, __, firstPageParam) => {
      if (firstPageParam <= 1) {
        return undefined
      }
      return firstPageParam - 1
    },
    enabled: isChatClientReady,
    queryFn: async ({ pageParam }) => {
      console.log('Fetching recent conversations, page:', chatClient.userID)
      const channels = await chatClient.queryChannels(
        { type: 'messaging', members: { $in: [chatClient.userID!] } },
        { last_message_at: -1 },
        { limit: PER_PAGE, offset: pageParam * PER_PAGE },
      )
      return channels.map((channel) => {
        const user = Object.values(channel.state.members).find(m => m.user?.id !== chatClient.userID)
        if (!user || !channel.data?.listing) {
          return null
        }
        return {
          id: channel.id,
          listing: channel.data.listing || { id: '', title: 'Nepoznato', picture: '' },
          user: { chat_uid: user.user_id, id: user.user?.id || '', name: user.user?.name || 'Nepoznati korisnik', avatar: user.user?.image || '' },
        }
      }).filter(n => !!n) as ChatConversation[]
    },
  })
}
