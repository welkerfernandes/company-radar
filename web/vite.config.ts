import {defineConfig} from 'vite';
export default defineConfig({build:{outDir:'../app/frontend',emptyOutDir:true},server:{proxy:{'/api':'http://127.0.0.1:8202','/docs':'http://127.0.0.1:8202'}}});
