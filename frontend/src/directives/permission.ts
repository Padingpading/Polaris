/** v-permission directive: hide element without required permission. */

import type { App, Directive } from 'vue'
import { useAuthStore } from '@/stores/auth'

const permissionDirective: Directive<HTMLElement, string | string[]> = {
  mounted(el, binding) {
    const authStore = useAuthStore()
    const value = binding.value
    if (!value) return
    const allowed = Array.isArray(value)
      ? authStore.hasAnyPermission(value)
      : authStore.hasPermission(value)
    if (!allowed) {
      el.parentNode?.removeChild(el)
    }
  },
}

export function setupPermissionDirective(app: App) {
  app.directive('permission', permissionDirective)
}
