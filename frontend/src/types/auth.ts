export enum OAuthProviders {
  GOOGLE = 'google',
  MICROSOFT = 'microsoft',
  APPLE = 'apple',
}

export interface GenericAPIResponse {
  detail?: string
  code: number
}
