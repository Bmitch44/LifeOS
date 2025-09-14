"use client"

import { Course } from "@/src/core/api/generated/types"
import { useDeleteCourse } from "@/src/features/school/courses/hooks/useCourses"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { CourseFormDialog } from "@/src/features/school/courses/components/CourseFormDialog"


export function CourseCard({ course }: { course: Course }) {
  const { mutate: deleteCourse } = useDeleteCourse()
  return (
    <Card>
      <CardHeader>
        <CardTitle>{course.name}</CardTitle>
      </CardHeader>
      <CardContent>
        <CourseFormDialog id={course.id!} edit={true} />
        <WarningDialog 
            title="Delete Course"
            description="Are you sure you want to delete this course?"
            onConfirm={() => deleteCourse(course.id!)}
        />
      </CardContent>
    </Card>
  )
}