<template>
	<div class="min-h-screen">
		<nav class="px-4 py-3 border-b border-slate-800 flex items-center justify-between bg-slate-950/60 backdrop-blur">
			<div class="font-semibold">Customer Insights</div>
			<div class="space-x-3 text-sm">
				<router-link class="hover:underline" to="/">Дашборд</router-link>
				<router-link class="hover:underline" to="/objects">Объекты</router-link>
				<router-link class="hover:underline" to="/engineer">Анкета</router-link>
				<router-link class="hover:underline" to="/reports">Отчеты</router-link>
			</div>
		</nav>
		<main class="p-4">
			<router-view />
		</main>
	</div>
</template>
