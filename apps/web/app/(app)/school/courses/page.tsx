import { CourseList } from "@/src/features/school/courses/components/CourseList"

export default function CoursesPage() {
  return (
  <div className="p-6 flex flex-col gap-4">
    <h1 className="text-2xl font-bold mb-4">Courses</h1>
    <CourseList />
  </div>
  )
}