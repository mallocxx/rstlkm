<template>
	<div class="min-h-screen">
		<nav class="border-b border-slate-800 bg-slate-950/60 backdrop-blur">
			<div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
				<div class="flex items-center gap-2">
					<div class="h-6 w-6 rounded bg-sky-500"></div>
					<div class="font-semibold tracking-tight">Customer Insights</div>
				</div>
				<div class="flex items-center gap-1 text-sm">
					<router-link to="/" class="px-3 py-2 rounded hover:bg-slate-800" active-class="bg-slate-800 text-white" exact-active-class="bg-slate-800 text-white">Дашборд</router-link>
					<router-link to="/objects" class="px-3 py-2 rounded hover:bg-slate-800" active-class="bg-slate-800 text-white">Объекты</router-link>
					<router-link to="/engineer" class="px-3 py-2 rounded hover:bg-slate-800" active-class="bg-slate-800 text-white">Анкета</router-link>
					<router-link to="/reports" class="px-3 py-2 rounded hover:bg-slate-800" active-class="bg-slate-800 text-white">Отчеты</router-link>
				</div>
			</div>
		</nav>
		<main class="px-4 py-6">
			<div class="max-w-7xl mx-auto">
				<router-view />
			</div>
		</main>
	</div>
</template>
