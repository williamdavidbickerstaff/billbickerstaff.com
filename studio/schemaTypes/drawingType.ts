import {defineField, defineType} from 'sanity'
import {DRAWING_CATEGORIES} from './drawingCategories'

export const drawingType = defineType({
  name: 'drawing',
  title: 'Drawing',
  type: 'document',
  fields: [
    defineField({
      name: 'photo',
      type: 'image',
    }),
    defineField({
      name: 'catagory',
      type: 'string',
      options: {
        // Add new categories in ./drawingCategories.ts
        list: [...DRAWING_CATEGORIES],
        layout: 'dropdown',
      },
    }),
  ],
})
