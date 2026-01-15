/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_STREAM_CHAT_API_KEY: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

interface Window {
  STREAM_CHAT_API_KEY?: string
}
