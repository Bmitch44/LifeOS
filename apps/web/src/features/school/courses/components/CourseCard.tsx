"use client"

import { Course } from "@/src/core/api/generated/types"
import { useDeleteCourse } from "@/src/features/school/courses/hooks/useCourses"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { CourseFormDialog } from "@/src/features/school/courses/components/CourseFormDialog"
import { useState } from "react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@workspace/ui/components/dropdown-menu"
import { Button } from "@workspace/ui/components/button"
import { MoreHorizontal, Calendar, MapPin, Building2, GraduationCap } from "lucide-react"
import { Badge } from "@workspace/ui/components/badge"
import { Avatar, AvatarFallback } from "@workspace/ui/components/avatar"


export function CourseCard({ course }: { course: Course }) {
  const { mutate: deleteCourse } = useDeleteCourse()
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)

  const handleDelete = () => {
    deleteCourse(course.id!)
    setDeleteOpen(false)
  }

  const professorInitial = (course.professor_name || "?").trim().charAt(0).toUpperCase()
  const hasGrade = course.final_grade !== null && course.final_grade !== undefined
  const gradeText = hasGrade ? String(course.final_grade) : "No grade"
  const gradeFirst = gradeText.charAt(0).toUpperCase()
  const gradeClass = gradeText === "No grade"
    ? "bg-muted text-muted-foreground"
    : gradeFirst === "A"
    ? "bg-emerald-100 text-emerald-700"
    : gradeFirst === "B"
    ? "bg-green-100 text-green-700"
    : gradeFirst === "C"
    ? "bg-yellow-100 text-yellow-800"
    : gradeFirst === "D"
    ? "bg-orange-100 text-orange-800"
    : "bg-red-100 text-red-700"

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <Badge className="bg-muted text-foreground/80">{course.code}</Badge>
              {course.credits != null && (
                <Badge className="bg-primary/10 text-primary">{course.credits} credits</Badge>
              )}
            </div>
            <CardTitle className="mt-1 truncate text-base sm:text-lg">{course.name}</CardTitle>
            <div className="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
              <Avatar className="h-6 w-6">
                <AvatarFallback className="text-[10px]">{professorInitial}</AvatarFallback>
              </Avatar>
              <div className="flex flex-col">
                <span className="truncate text-xs">{course.professor_name}</span>
                  {course.professor_email && (
                    <span className="hidden sm:inline text-foreground/60 text-xs">{course.professor_email}</span>
                  )}
              </div>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <Badge className={`px-2 ${gradeClass}`}>{gradeText}</Badge>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="hover:bg-muted/60">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem onClick={() => setEditOpen(true)}>Edit</DropdownMenuItem>
                <DropdownMenuItem className="text-destructive" onClick={() => setDeleteOpen(true)}>Delete</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </CardHeader>
      <CardContent className="grid grid-cols-1 gap-3 text-sm sm:grid-cols-2">
        {course.semester || course.year ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Calendar className="h-4 w-4" />
            <span>{[course.semester, course.year].filter(Boolean).join(" ")}</span>
          </div>
        ) : null}

        {course.department ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <Building2 className="h-4 w-4" />
            <span className="truncate">{course.department}</span>
          </div>
        ) : null}

        {(course.campus || course.location) ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <MapPin className="h-4 w-4" />
            <span className="truncate">{[course.campus, course.location].filter(Boolean).join(" • ")}</span>
          </div>
        ) : null}

        {course.credits != null ? (
          <div className="flex items-center gap-2 text-muted-foreground">
            <GraduationCap className="h-4 w-4" />
            <span>{course.credits} credits</span>
          </div>
        ) : null}

        {course.description ? (
          <p className="col-span-1 sm:col-span-2 text-foreground/80">{course.description}</p>
        ) : null}

        <CourseFormDialog id={course.id!} edit={true} open={editOpen} setOpen={setEditOpen} />
        <WarningDialog
          title="Delete Course"
          description="Are you sure you want to delete this course?"
          onConfirm={handleDelete}
          open={deleteOpen}
          setOpen={setDeleteOpen}
        />
      </CardContent>
    </Card>
  )
}