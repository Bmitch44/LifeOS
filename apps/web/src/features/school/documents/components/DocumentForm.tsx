"use client"

import { z } from "zod"
import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { Button } from "@workspace/ui/components/button"
import { useCreateDocument, useGetDocument, useUpdateDocument } from "../hooks/useDocuments"

const formSchema = z.object({
  name: z.string(),
  description: z.string().optional().nullable(),
  file_url: z.string(),
  file_type: z.string().optional().nullable(),
  size: z.coerce.number().int().min(0).optional().nullable(),
})

export function DocumentForm({ id, edit, setOpen }: { id: number, edit: boolean, setOpen: (open: boolean) => void }) {
  const { data: document, isPending } = useGetDocument(id, edit)
  const { mutate: updateDocument } = useUpdateDocument()
  const { mutate: createDocument } = useCreateDocument()

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: "",
      description: "",
      file_url: "",
      file_type: "",
      size: 0,
    },
  })

  useEffect(() => {
    if (edit && document) {
      form.reset({
        name: document.name ?? "",
        description: document.description ?? "",
        file_url: document.file_url ?? "",
        file_type: document.file_type ?? "",
        size: document.size ?? 0,
      })
    }
  }, [edit, document, form])

  if (edit && isPending) return <div>Loading…</div>

  const onSubmit = (data: z.infer<typeof formSchema>) => {
    if (edit) {
      updateDocument({ id, body: data })
    } else {
      createDocument(data)
    }
    setOpen(false)
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
          <FormField control={form.control} name="file_url" render={({ field }) => (
            <FormItem>
              <FormLabel>File URL</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )} />
          <FormField control={form.control} name="file_type" render={({ field }) => (
            <FormItem>
              <FormLabel>File Type</FormLabel>
              <FormControl>
                <Input {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )} />
          <FormField control={form.control} name="size" render={({ field }) => (
            <FormItem>
              <FormLabel>Size</FormLabel>
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

