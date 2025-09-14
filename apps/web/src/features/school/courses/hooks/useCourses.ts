"use client"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { PaginatedCourses, Course, CourseCreate, CourseUpdate } from "@/src/core/api/generated/types"
import { api } from "@/src/core/api/client"
import { useAuthToken } from "@/src/core/auth/useAuthToken"

export function useAllCourses(page = 1, size = 20) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["courses", page, size],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<PaginatedCourses>(`/v1/courses?page=${page}&size=${size}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    staleTime: 30_000,
  })
}

export function useGetCourse(id: number, enabled: boolean = true) {
  const getToken = useAuthToken()
  return useQuery({
    queryKey: ["courses", id],
    queryFn: async () => {
      const token = await getToken()
      return api.getJson<Course>(`/v1/courses/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    enabled: enabled,
  })
}

export function useCreateCourse() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (body: CourseCreate) => {
      const token = await getToken()
      return api.postJson<Course>(`/v1/courses`, body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }),
  })
}

export function useUpdateCourse() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (payload: { id: number, body: CourseUpdate }) => {
      const token = await getToken()
      return api.putJson<Course>(`/v1/courses/${payload.id}`, payload.body, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["courses"] }),
  })
}

export function useDeleteCourse() {
  const qc = useQueryClient()
  const getToken = useAuthToken()
  return useMutation({
    mutationFn: async (id: number) => {
      const token = await getToken()
      return api.deleteJson<{message: string}>(`/v1/courses/${id}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : undefined,
      })
    },
  })
}