<template>
  <div class="flex h-screen bg-gray-900 text-white">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 flex-shrink-0">
      <div class="p-4 border-b border-gray-700">
        <h1 class="text-2xl font-bold">Admin Panel</h1>
      </div>
      <nav class="p-4">
        <ul class="space-y-2">
          <li>
            <router-link to="/admin/dashboard" class="flex items-center px-4 py-2 rounded-md hover:bg-gray-700" active-class="bg-indigo-600">
              Dashboard
            </router-link>
          </li>
          <li>
            <router-link to="/admin/users" class="flex items-center px-4 py-2 rounded-md hover:bg-gray-700" active-class="bg-indigo-600">
              Users
            </router-link>
          </li>
          <li>
            <router-link to="/admin/challenges" class="flex items-center px-4 py-2 rounded-md hover:bg-gray-700" active-class="bg-indigo-600">
              Challenges
            </router-link>
          </li>
          <li>
            <router-link to="/admin/settings" class="flex items-center px-4 py-2 rounded-md hover:bg-gray-700" active-class="bg-indigo-600">
              Settings
            </router-link>
          </li>
          <li>
             <router-link to="/" class="flex items-center px-4 py-2 rounded-md hover:bg-gray-700 text-sm text-gray-400 mt-8">
              &larr; Back to Site
            </router-link>
          </li>
        </ul>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="p-8">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
// This is a layout component, so it typically won't have complex logic.
</script>
