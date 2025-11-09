class PermissionsProvider {
  private permissions: Set<string>

  constructor(initialPermissions: string[] = []) {
    this.permissions = new Set(initialPermissions)
  }

  can(permission: string): boolean {
    return this.permissions.has(permission)
  }

  update(newPermissions: string[]): void {
    this.permissions = new Set(newPermissions)
  }
}

export const permissionsProvider = new PermissionsProvider()

export function can(permission: string): boolean {
  return permissionsProvider.can(permission)
}

export function updatePermissions(newPermissions: string[]): void {
  permissionsProvider.update(newPermissions)
}
