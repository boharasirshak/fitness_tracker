import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, loadEnv } from 'vite';

export default () => {
  process.env = {...process.env, ...loadEnv('public', process.cwd())};

  return defineConfig({
    plugins: [sveltekit()],
  });
}

