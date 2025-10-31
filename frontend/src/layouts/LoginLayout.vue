<template>
  <div class="flex min-h-screen">
    <div class="flex-1 xl:block hidden">
      <slot name="preview"/>
    </div>
    <div class="flex-1 grid place-items-center">
      <slot/>
    </div>
  </div>
</template>
