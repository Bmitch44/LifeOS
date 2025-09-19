"use client"
import { useAllCourses } from "@/src/features/school/courses/hooks/useCourses"
import { Course } from "@/src/core/api/generated/types"
import { CourseCard } from "@/src/features/school/courses/components/CourseCard"
import { CourseFormDialog } from "@/src/features/school/courses/components/CourseFormDialog"
import { useState } from "react"


export function CourseList() {
  const [addOpen, setAddOpen] = useState(false)
  const { data, isPending, error } = useAllCourses()
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load courses</div>

  return (
    <div className="flex flex-col gap-4"> 
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Courses</h1>
        <CourseFormDialog id={0} edit={false} open={addOpen} setOpen={setAddOpen} />
      </div>
      {data?.items?.map((course: Course) => (
        <div key={course.id} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <CourseCard course={course} />
        </div>
      ))}
    </div>
  )
}


