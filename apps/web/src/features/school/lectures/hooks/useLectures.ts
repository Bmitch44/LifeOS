"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { PaginatedLectures, Lecture, LectureCreate, LectureUpdate } from "@/src/core/api/generated/types"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export function useAllLectures(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["lectures", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<PaginatedLectures>(`/v1/lectures?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useGetLecture(id: number, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["lectures", id],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<Lecture>(`/v1/lectures/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled: enabled,
  })
}

export function useCreateLecture() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: LectureCreate) => {
      const token = await getToken()
      return api.postJson<Lecture>(`/v1/lectures`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["lectures"] }),
  })
}

export function useUpdateLecture() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number, body: LectureUpdate }) => {
      const token = await getToken()
      return api.putJson<Lecture>(`/v1/lectures/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["lectures"] }),
  })
}

export function useDeleteLecture() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{message: string}>(`/v1/lectures/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["lectures"] }),
  })
}