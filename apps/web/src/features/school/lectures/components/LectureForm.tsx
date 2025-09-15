"use client"

import { z } from "zod"
import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { useCreateLecture, useGetLecture, useUpdateLecture } from "../hooks/useLectures"
import { Button } from "@workspace/ui/components/button"

const formSchema = z.object({
  course_id: z.coerce.number().int().min(1),
  name: z.string(),
  description: z.string(),
  start_date: z.coerce.date(),
  end_date: z.coerce.date(),
  weight: z.coerce.number().min(0),
  final_grade: z.coerce.number().min(0).max(100),
})

export function LectureForm({ id, edit, setOpen }: { id: number, edit: boolean, setOpen: (open: boolean) => void }) {
    const { data: lecture, isPending } = useGetLecture(id, edit)
    const { mutate: updateLecture } = useUpdateLecture()
    const { mutate: createLecture } = useCreateLecture()

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            course_id: 0,
            name: "",
            description: "",
            start_date: new Date(),
            end_date: new Date(),
            weight: 0,
            final_grade: 0,
        }
    })

    useEffect(() => {
        if (edit && lecture) {
            form.reset({
                course_id: lecture.course_id ?? 0,
                name: lecture.name ?? "",
                description: lecture.description ?? "",
                start_date: lecture.start_date ? new Date(lecture.start_date) : new Date(),
                end_date: lecture.end_date ? new Date(lecture.end_date) : new Date(),
                weight: lecture.weight ?? 0,
                final_grade: lecture.final_grade ?? 0,
            })
        }
    }, [edit, lecture, form])

    if (edit && isPending) return <div>Loading…</div>

    const onSubmit = (data: z.infer<typeof formSchema>) => {
        const payload = {
          ...data,
          start_date: data.start_date.toISOString(),
          end_date: data.end_date.toISOString(),
        } as any
        if (edit) {
            updateLecture({ id, body: payload })
        } else {
            createLecture(payload)
        }
        setOpen(false)
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <div className="grid grid-cols-2 gap-4">
                <FormField control={form.control} name="course_id" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Course Id</FormLabel>
                        <FormControl>
                            <Input {...field} type="number" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
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
                            <Input type="datetime-local" value={field.value ? new Date(field.value).toISOString().slice(0,16) : ""} onChange={(e) => field.onChange(new Date(e.target.value))} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="end_date" render={({ field }) => (
                    <FormItem>
                        <FormLabel>End Date</FormLabel>
                        <FormControl>
                            <Input type="datetime-local" value={field.value ? new Date(field.value).toISOString().slice(0,16) : ""} onChange={(e) => field.onChange(new Date(e.target.value))} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="weight" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Weight</FormLabel>
                        <FormControl>
                            <Input {...field} type="number" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="final_grade" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Final Grade</FormLabel>
                        <FormControl>
                            <Input {...field} type="number" />
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

