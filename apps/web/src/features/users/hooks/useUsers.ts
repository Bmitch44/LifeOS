"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import type { paths } from "@/src/core/api/generated/schema"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

type UsersListResp = any // replace when contracts define /v1/users

export function useUsers(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["users", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<UsersListResp>(`/v1/users?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useCreateUser() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: unknown) => {
      const token = await getToken()
      return api.postJson(`/v1/users`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["users"] }),
  })
}


