/** Role and permission API. */

import { request } from '@/api/http'
import type { PermissionItem, RoleCreatePayload, RoleItem, RoleUpdatePayload } from '@/types'

export function listRolesApi() {
  return request<RoleItem[]>({
    url: '/roles',
    method: 'get',
  })
}

export function listPermissionsApi() {
  return request<PermissionItem[]>({
    url: '/roles/permissions',
    method: 'get',
  })
}

export function createRoleApi(data: RoleCreatePayload) {
  return request<RoleItem>({
    url: '/roles',
    method: 'post',
    data,
  })
}

export function updateRoleApi(roleId: number, data: RoleUpdatePayload) {
  return request<RoleItem>({
    url: `/roles/${roleId}`,
    method: 'put',
    data,
  })
}

export function deleteRoleApi(roleId: number) {
  return request<null>({
    url: `/roles/${roleId}`,
    method: 'delete',
  })
}
