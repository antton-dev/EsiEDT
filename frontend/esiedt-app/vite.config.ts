import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';


export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) => filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},

			// adapter-auto only supports some environments, see https://svelte.dev/docs/kit/adapter-auto for a list.
			// If your environment is not supported, or you settled on a specific environment, switch out the adapter.
			// See https://svelte.dev/docs/kit/adapters for more information about adapters.
			adapter: adapter({
				pages: 'build',
				assets: 'build',
				fallback: 'index.html',
				precompress: false,
				strict: true
			})
		}),
		SvelteKitPWA({
			registerType: "autoUpdate",
			manifest: {
				name: "EsiEDT",
				short_name: "EsiEDT",
				description: "Emploi du temps pour l'Esisar, par et pour les étudiants",
				theme_color: "#6d28d9;",
				background_color: "#ffffff",
				display: "standalone",
				start_url: "/",
				icons: [
					{src: "icon-192.png", sizes: '192x192', type: "image/png"},
					{src: "icon-512.png", sizes: '512x512', type: "image/png"},
					{src: "icon-512.png", sizes: '512x512', type: "image/png", purpose: "maskable"}
				]
			},
			workbox: {
				runtimeCaching: [
					{
						urlPattern: ({ url }) => url.pathname.startsWith('/api/schedule'),
						handler: "NetworkFirst",
						options: {
							cacheName: "schedule-cache",
							networkTimeoutSeconds: 5,
							expiration: {maxEntries: 20, maxAgeSeconds: 60*60*24*7}
						}
					},
					{
						urlPattern : ({ url }) => url.pathname.startsWith('/api/groups'),
						handler: 'CacheFirst',
						options: {
							cacheName: 'groups-cache',
							expiration: { maxEntries: 5, maxAgeSeconds: 60 * 60 * 24 * 30 } // 30 jours
						}
					}
				]
			},
			devOptions: {
				enabled: false
			}
		})
	],
	// preview: {
	// 	allowedHosts: true
	// }
});
