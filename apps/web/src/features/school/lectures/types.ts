export type Lecture = {
  id?: number | null
  course_id: number
  name: string
  description: string
  start_date: string
  end_date: string
  weight: number
  final_grade: number
  created_at?: string
  updated_at?: string
}

export type LectureCreate = Omit<Lecture, "id" | "created_at" | "updated_at">
export type LectureUpdate = LectureCreate

export type PaginatedLectures = {
  items: Lecture[]
  page: number
  size: number
  total: number
}

