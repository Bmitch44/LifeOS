"use client"
import { UserList } from "@/src/features/users/components/UserList"
import { CourseList } from "@/src/features/school/courses/components/CourseList"
import { AssesmentList } from "@/src/features/school/assesments/components/AssesmentList"
import { LectureList } from "@/src/features/school/lectures/components/LectureList"

export default function Page() {
  return (
    <div className="p-6 flex flex-col gap-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <UserList />
      <CourseList />
      <AssesmentList />
      <LectureList />
    </div>
  )
}


