import type * as z from 'zod'
import type {
  activeUserSchema,
  associationSchema,
  userBasicInfoSchema,
} from '@/schemas/user.ts'

export type UserSchemaState = z.output<typeof activeUserSchema>
export type DonorUser = UserSchemaState & { role: 'donor' }
export type RecipientIndividualUser = UserSchemaState & { role: 'recipient_individual' }
export type RecipientAssociationUser = UserSchemaState
  & { role: 'recipient_association' } & z.output<typeof associationSchema>
export type NewUser = Partial<UserSchemaState> & { role: undefined }

export type User
  = DonorUser
    | RecipientIndividualUser
    | RecipientAssociationUser
    | NewUser

export type UserBasicInfo = z.infer<typeof userBasicInfoSchema>
export type UserAssociationInfo = z.infer<typeof associationSchema>
