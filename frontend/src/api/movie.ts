/** Movie management API. */

import { request } from '@/api/http'
import type { MovieCreatePayload, MovieItem, MovieUpdatePayload, PageResult } from '@/types'

export interface MovieListQuery {
  keyword?: string
  genre?: string
  is_active?: boolean
  page: number
  page_size: number
}

export function listMoviesApi(params: MovieListQuery) {
  return request<PageResult<MovieItem>>({
    url: '/movies',
    method: 'get',
    params,
  })
}

export function getMovieApi(movieId: number) {
  return request<MovieItem>({
    url: `/movies/${movieId}`,
    method: 'get',
  })
}

export function createMovieApi(data: MovieCreatePayload) {
  return request<MovieItem>({
    url: '/movies',
    method: 'post',
    data,
  })
}

export function updateMovieApi(movieId: number, data: MovieUpdatePayload) {
  return request<MovieItem>({
    url: `/movies/${movieId}`,
    method: 'put',
    data,
  })
}

export function deleteMovieApi(movieId: number) {
  return request<null>({
    url: `/movies/${movieId}`,
    method: 'delete',
  })
}
