"use client"

import { z } from "zod"
import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { useCreateCourse, useGetCourse, useUpdateCourse } from "../hooks/useCourses"
import { Button } from "@workspace/ui/components/button"

const formSchema = z.object({
  name: z.string(),
  description: z.string(),
  code: z.string(),
  professor_name: z.string(),
  professor_email: z.string(),
  credits: z.coerce.number().int().min(1).max(10),
  semester: z.string(),
  year: z.coerce.number().int().min(2000),
  department: z.string(),
  campus: z.string(),
  location: z.string(),
  final_grade: z.coerce.number().min(0).max(100),
})

export function CourseForm({ id, edit }: { id: number, edit: boolean }) {
    
    const { data: course, isPending } = useGetCourse(id, edit)
    const { mutate: updateCourse } = useUpdateCourse()
    const { mutate: createCourse } = useCreateCourse()


    // Initialize the form unconditionally to keep hook order stable
    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            name: "",
            description: "",
            code: "",
            professor_name: "",
            professor_email: "",
            credits: 0,
            semester: "",
            year: 2000,
            department: "",
            campus: "",
            location: "",
            final_grade: 0,
        }
    })

    // When editing and the course loads, populate the form
    useEffect(() => {
        if (edit && course) {
            form.reset({
                name: course.name ?? "",
                description: course.description ?? "",
                code: course.code ?? "",
                professor_name: course.professor_name ?? "",
                professor_email: course.professor_email ?? "",
                credits: course.credits ?? 0,
                semester: course.semester ?? "",
                year: course.year ?? 2000,
                department: course.department ?? "",
                campus: course.campus ?? "",
                location: course.location ?? "",
                final_grade: course.final_grade ?? 0,
            })
        }
    }, [edit, course, form])

    if (edit && isPending) return <div>Loading…</div>


    const onSubmit = (data: z.infer<typeof formSchema>) => {
        if (edit) {
            updateCourse({ id, body: data })
        } else {
            createCourse(data)
        }
    }

    return (

        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
                <div className="grid grid-cols-2 gap-4">
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
                <FormField control={form.control} name="code" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Code</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="professor_name" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Professor Name</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="professor_email" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Professor Email</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="credits" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Credits</FormLabel>
                        <FormControl>
                            <Input {...field} type="number" />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="semester" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Semester</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                        <FormMessage />
                    </FormItem>
                )} />
                <FormField control={form.control} name="year" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Year</FormLabel>
                        <FormControl>
                            <Input {...field} type="number" />
                        </FormControl>
                    </FormItem>
                )} />
                <FormField control={form.control} name="department" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Department</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                    </FormItem>
                )} />
                <FormField control={form.control} name="campus" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Campus</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
                    </FormItem>
                )} />
                <FormField control={form.control} name="location" render={({ field }) => (
                    <FormItem>
                        <FormLabel>Location</FormLabel>
                        <FormControl>
                            <Input {...field} />
                        </FormControl>
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