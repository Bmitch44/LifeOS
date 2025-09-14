"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { PaginatedUsers, User, UserUpdate } from "@/src/core/api/generated/types"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export function useAllUsers(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["users", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<PaginatedUsers>(`/v1/users?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useGetUser(id: number, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["users", id],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<User>(`/v1/users/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled: enabled
  })
}

// export function useCreateUser() {
//   const qc = useQueryClient()
//   const getToken = useAuthToken()
//   return useMutation({
//     mutationFn: async (body: UserCreate) => {
//       const token = await getToken()
//       return api.postJson<User>(`/v1/users`, body, {
//         headers: token ? { Authorization: `Bearer ${token}` } : undefined,
//       })
//     },
//     onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
//   })
// }

export function useUpdateUser() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number, body: UserUpdate }) => {
      const token = await getToken()
      return api.putJson<User>(`/v1/users/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  })
}

export function useDeleteUser() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{message: string}>(`/v1/users/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  })
}


