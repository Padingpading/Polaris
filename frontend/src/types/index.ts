/** Shared TypeScript domain types. */

export interface ApiResponse<T = unknown> {
  code: number
  message: string
  data: T
}

export interface PageResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface UserBrief {
  id: number
  username: string
  email: string
  full_name?: string | null
  is_superuser: boolean
  roles: string[]
  permissions: string[]
}

export interface RoleBrief {
  id: number
  code: string
  name: string
}

export interface UserItem {
  id: number
  username: string
  email: string
  full_name?: string | null
  is_active: boolean
  is_superuser: boolean
  roles: RoleBrief[]
  created_at: string
  updated_at: string
}

export interface PermissionItem {
  id: number
  code: string
  name: string
  description?: string | null
}

export interface RoleItem {
  id: number
  code: string
  name: string
  description?: string | null
  permissions: PermissionItem[]
  created_at: string
  updated_at: string
}

export interface LoginResult {
  access_token: string
  token_type: string
  expires_in: number
  user: UserBrief
}

export interface UserCreatePayload {
  username: string
  email: string
  password: string
  full_name?: string
  is_active: boolean
  role_ids: number[]
}

export interface UserUpdatePayload {
  email?: string
  full_name?: string
  is_active?: boolean
  password?: string
  role_ids?: number[]
}

export interface RoleCreatePayload {
  code: string
  name: string
  description?: string
  permission_ids: number[]
}

export interface RoleUpdatePayload {
  name?: string
  description?: string
  permission_ids?: number[]
}

export interface MovieItem {
  id: number
  title: string
  director?: string | null
  genre?: string | null
  release_year?: number | null
  duration_minutes?: number | null
  rating?: number | string | null
  description?: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface MovieCreatePayload {
  title: string
  director?: string
  genre?: string
  release_year?: number
  duration_minutes?: number
  rating?: number
  description?: string
  is_active: boolean
}

export interface MovieUpdatePayload {
  title?: string
  director?: string
  genre?: string
  release_year?: number
  duration_minutes?: number
  rating?: number
  description?: string
  is_active?: boolean
}
