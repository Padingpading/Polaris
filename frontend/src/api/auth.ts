/** Auth API. */

import { request } from '@/api/http'
import type { LoginResult, UserBrief } from '@/types'

export function loginApi(username: string, password: string) {
  return request<LoginResult>({
    url: '/auth/login',
    method: 'post',
    data: { username, password },
  })
}

export function logoutApi() {
  return request<null>({
    url: '/auth/logout',
    method: 'post',
  })
}

export function getMeApi() {
  return request<UserBrief>({
    url: '/auth/me',
    method: 'get',
  })
}
