/** User management API. */

import { request } from '@/api/http'
import type { PageResult, UserCreatePayload, UserItem, UserUpdatePayload } from '@/types'

export interface UserListQuery {
  keyword?: string
  is_active?: boolean
  page: number
  page_size: number
}

export function listUsersApi(params: UserListQuery) {
  return request<PageResult<UserItem>>({
    url: '/users',
    method: 'get',
    params,
  })
}

export function getUserApi(userId: number) {
  return request<UserItem>({
    url: `/users/${userId}`,
    method: 'get',
  })
}

export function createUserApi(data: UserCreatePayload) {
  return request<UserItem>({
    url: '/users',
    method: 'post',
    data,
  })
}

export function updateUserApi(userId: number, data: UserUpdatePayload) {
  return request<UserItem>({
    url: `/users/${userId}`,
    method: 'put',
    data,
  })
}

export function deleteUserApi(userId: number) {
  return request<null>({
    url: `/users/${userId}`,
    method: 'delete',
  })
}
