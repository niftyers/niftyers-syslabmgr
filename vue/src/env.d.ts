/// <reference types="vite/client" />
/// <reference types="vite-plugin-vue-devtools/global" />

interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

export {}

import 'vite/client'
import 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    auth: boolean
  }
}
