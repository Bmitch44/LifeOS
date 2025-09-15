"use client"

import type { Lecture } from "../../lectures/types"
import { useDeleteLecture } from "@/src/features/school/lectures/hooks/useLectures"
import { WarningDialog } from "@/components/dialogs/WarningDialog"
import { Card, CardHeader, CardTitle, CardContent } from "@workspace/ui/components/card"
import { LectureFormDialog } from "@/src/features/school/lectures/components/LectureFormDialog"
import { useState } from "react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@workspace/ui/components/dropdown-menu"
import { Button } from "@workspace/ui/components/button"
import { MoreHorizontal, Calendar } from "lucide-react"
import { Badge } from "@workspace/ui/components/badge"


export function LectureCard({ lecture }: { lecture: Lecture }) {
  const { mutate: deleteLecture } = useDeleteLecture()
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [editOpen, setEditOpen] = useState(false)

  const handleDelete = () => {
    deleteLecture(lecture.id!)
    setDeleteOpen(false)
  }

  const hasGrade = lecture.final_grade !== null && lecture.final_grade !== undefined
  const gradeText = hasGrade ? String(lecture.final_grade) : "No grade"

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <Badge className="bg-muted text-foreground/80">{lecture.course_id}</Badge>
            </div>
            <CardTitle className="mt-1 truncate text-base sm:text-lg">{lecture.name}</CardTitle>
            <div className="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
              <Calendar className="h-4 w-4" />
              <span>{[lecture.start_date, lecture.end_date].filter(Boolean).join(" → ")}</span>
            </div>
          </div>

          <div className="flex items-start gap-2">
            <Badge className="px-2">{gradeText}</Badge>
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
        {lecture.description ? (
          <p className="col-span-1 sm:col-span-2 text-foreground/80">{lecture.description}</p>
        ) : null}

        <LectureFormDialog id={lecture.id!} edit={true} open={editOpen} setOpen={setEditOpen} />
        <WarningDialog
          title="Delete Lecture"
          description="Are you sure you want to delete this lecture?"
          onConfirm={handleDelete}
          open={deleteOpen}
          setOpen={setDeleteOpen}
        />
      </CardContent>
    </Card>
  )
}

