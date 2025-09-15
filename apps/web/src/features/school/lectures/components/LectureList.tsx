"use client"
import { useAllLectures } from "@/src/features/school/lectures/hooks/useLectures"
import type { Lecture } from "../../lectures/types"
import { LectureCard } from "@/src/features/school/lectures/components/LectureCard"
import { LectureFormDialog } from "./LectureFormDialog"
import { useState } from "react"


export function LectureList() {
  const [addOpen, setAddOpen] = useState(false)
  const { data, isPending, error } = useAllLectures()
  if (isPending) return <div>Loading…</div>
  if (error) return <div>Failed to load lectures</div>

  return (
    <div className="flex flex-col gap-4"> 
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Lectures</h1>
        <LectureFormDialog id={0} edit={false} open={addOpen} setOpen={setAddOpen} />
      </div>
      {data?.items?.map((lecture: Lecture) => (
        <div key={lecture.id} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <LectureCard lecture={lecture} />
        </div>
      ))}
    </div>
  )
}



