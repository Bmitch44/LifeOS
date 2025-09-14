"use client"

import { Course } from "@/src/core/api/generated/types"
import { useDeleteCourse } from "@/src/features/school/courses/hooks/useCourses"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { CourseFormDialog } from "@/src/features/school/courses/components/CourseFormDialog"
import { useState } from "react"


export function CourseCard({ course }: { course: Course }) {
  const { mutate: deleteCourse } = useDeleteCourse()
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)
  return (
    <Card>
      <CardHeader>
        <CardTitle>{course.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex justify-between items-center w-full">
          <CourseFormDialog id={course.id!} edit={true} open={editOpen} setOpen={setEditOpen} />
          <WarningDialog 
              title="Delete Course"
              description="Are you sure you want to delete this course?"
              onConfirm={() => deleteCourse(course.id!)}
              open={deleteOpen}
              setOpen={setDeleteOpen}
          />
        </div>
      </CardContent>
    </Card>
  )
}