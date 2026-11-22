// Single source of truth for drawing categories.
// Used by the Studio schema (drawingType.ts) AND the website's drawings page,
// so adding a category here makes it appear on the site automatically
// (once at least one drawing uses it).
//
// `value` is what's stored on the document — keep it unique and don't change it
// once drawings use it. `title` is shown in the Studio and as the page heading.
// The order here is the order sections appear on the page.
export const DRAWING_CATEGORIES = [
  {title: 'Lawns', value: 'lawn'},
  {title: 'Animals', value: 'animals'},
  {title: 'Landscape', value: 'landscape'},
  {title: 'Buildings', value: 'buildings'},
  {title: 'Boats', value: 'boats'},
] as const
