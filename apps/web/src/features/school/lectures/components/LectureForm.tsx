"use client"

import { z } from "zod"
import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { useCreateLecture, useGetLecture, useUpdateLecture } from "@/src/features/school/lectures/hooks/useLectures"
import { Button } from "@workspace/ui/components/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@workspace/ui/components/select"
import { useAllCourses } from "../../courses/hooks/useCourses"

const formSchema = z.object({
    course_id: z.coerce.number().min(1, "Select a course"),
    name: z.string(),
    description: z.string(),
    start_date: z.string(),
    end_date: z.string(),
})

export function LectureForm({ id, edit, setOpen }: { id: number, edit: boolean, setOpen: (open: boolean) => void }) {
    
    const { data: lecture, isPending } = useGetLecture(id, edit)
    const { mutate: updateLecture } = useUpdateLecture()
    const { mutate: createLecture } = useCreateLecture()
    const { data: courses, isPending: isCoursesPending } = useAllCourses(1, 100)

    // Initialize the form unconditionally to keep hook order stable
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            course_id: 0,
            name: "",
            description: "",
            start_date: "",
            end_date: "",
        }
    })

    // When editing and the course loads, populate the form
    useEffect(() => {
        if (edit && lecture) {
            form.reset({
                course_id: lecture.course_id ?? 0,
                name: lecture.name ?? "",
                description: lecture.description ?? "",
                start_date: lecture.start_date ?? "",
                end_date: lecture.end_date ?? "",
            })
        }
    }, [edit, lecture, form])

    if (edit && isPending || isCoursesPending) return <div>Loading…</div>


    const onSubmit = (data: z.infer<typeof formSchema>) => {
        if (edit) {
            updateLecture({ id, body: data })
        } else {
            createLecture({ ...data })
        }
        setOpen(false)
    }

    return (

        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <div className="grid grid-cols-2 gap-4">
                <FormField
                    control={form.control}
                    name="course_id"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Course</FormLabel>
                            <FormControl>
                                <Select
                                    value={field.value && field.value !== 0 ? String(field.value) : undefined}
                                    onValueChange={(val) => field.onChange(Number(val))}
                               >
                                    <SelectTrigger className="w-full">
                                        <SelectValue placeholder="Select a course" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {courses?.items?.map((c) => (
                                            <SelectItem key={c.id ?? undefined} value={String(c.id ?? "")}>
                                                {c.code} — {c.name}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField control={form.control} name="name" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Name</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="description" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Description</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="start_date" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Start Date</FormLabel>
                        <FormControl>
                            <Input {...field} type="date" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="end_date" render={({ field }) => (
                    <FormItem>
                        <FormLabel>End Date</FormLabel>
                        <FormControl>
                            <Input {...field} type="date" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />   
                </div>
                <Button type="submit">{edit ? "Update" : "Create"}</Button>
            </form>
        </Form>
    )
}