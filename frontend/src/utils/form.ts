export function objectToFormData(obj: Record<string, any>, rootName = '', ignoreList: string[] = []) {
  const formData = new FormData()

  function appendFormData(data: any, root: string) {
    if (!ignore(root)) {
      root = root || ''
      if (data instanceof File) {
        formData.append(root, data)
      }
      else if (Array.isArray(data)) {
        for (let i = 0; i < data.length; i++) {
          appendFormData(data[i], `${root}[${i}]`)
        }
      }
      else if (typeof data === 'object' && data) {
        for (const key in data) {
          if (Object.prototype.hasOwnProperty.call(data, key)) {
            if (root === '') {
              appendFormData(data[key], key)
            }
            else {
              appendFormData(data[key], `${root}.${key}`)
            }
          }
        }
      }
      else {
        if (data !== null && typeof data !== 'undefined') {
          formData.append(root, data)
        }
      }
    }
  }

  function ignore(root: string) {
    return Array.isArray(ignoreList)
      && ignoreList.includes(root)
  }

  appendFormData(obj, rootName)

  return formData
}
