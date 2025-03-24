<!-- src/App.vue -->
<template>
  <mainpage_template /> <!-- 渲染全局布局 -->
</template>

<script>
import mainpage_template from './components/mainpage_template.vue';

export default {
  name: 'App',
  components: {
    mainpage_template, // 引入布局组件
  },
};


</script>
