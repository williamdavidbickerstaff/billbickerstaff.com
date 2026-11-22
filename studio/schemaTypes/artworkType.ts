import {defineField, defineType} from 'sanity'

export const artworkType = defineType({
  name: 'artwork',
  title: 'Artwork',
  type: 'document',
  fields: [
    defineField({
      name: 'slug',
      type: 'slug',
    }),
    defineField({
      name: 'name',
      type: 'string',
    }),
    defineField({
      name: 'media',
      type: 'string',
    }),
    defineField({
      name: 'dimensions',
      type: 'string',
    }),
    defineField({
      name: 'description',
      type: 'string',
    }),
    defineField({
      name: 'photo',
      type: 'image',
    }),
    defineField({
      name: 'date',
      type: 'date',
    }),
  ],
})
