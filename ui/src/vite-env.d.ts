/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_SYMBOLS: string;
    readonly VITE_WEBSOCKET_URL: string; 
    readonly VITE_EXCHANGES: string;
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}