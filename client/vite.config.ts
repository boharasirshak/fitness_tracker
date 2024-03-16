import react from '@vitejs/plugin-react-swc';
import { defineConfig, loadEnv } from 'vite';

export default () => {
  process.env = {...process.env, ...loadEnv('public', process.cwd())};

  return defineConfig({
    plugins: [react()],
  });
}
