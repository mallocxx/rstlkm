<template>
	<div class="min-h-screen">
		<nav class="border-b border-gray-200 bg-white shadow-sm">
			<div class="max-w-7xl mx-auto px-3 sm:px-4 py-3 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<div class="h-6 w-6 rounded bg-sky-500"></div>
					<div class="font-semibold tracking-tight text-gray-900">Customer Insights</div>
				</div>
				<div class="flex flex-wrap items-center gap-1 text-sm">
					<router-link to="/" class="px-2 sm:px-3 py-2 rounded hover:bg-gray-100 text-gray-700" active-class="bg-gray-100 text-gray-900 font-medium" exact-active-class="bg-gray-100 text-gray-900 font-medium">Дашборд</router-link>
					<router-link to="/objects" class="px-2 sm:px-3 py-2 rounded hover:bg-gray-100 text-gray-700" active-class="bg-gray-100 text-gray-900 font-medium">Объекты</router-link>
					<router-link to="/engineer" class="px-2 sm:px-3 py-2 rounded hover:bg-gray-100 text-gray-700" active-class="bg-gray-100 text-gray-900 font-medium">Анкета</router-link>
					<router-link to="/reports" class="px-2 sm:px-3 py-2 rounded hover:bg-gray-100 text-gray-700" active-class="bg-gray-100 text-gray-900 font-medium">Отчеты</router-link>
				</div>
			</div>
		</nav>
		<main class="px-3 sm:px-4 py-4 sm:py-6">
			<div class="max-w-7xl mx-auto">
				<router-view />
			</div>
		</main>
	</div>
</template>
