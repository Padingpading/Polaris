<template>
  <div class="dashboard">
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card shadow="never">
          <div class="stat-label">当前用户</div>
          <div class="stat-value">{{ authStore.displayName }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div class="stat-label">角色</div>
          <div class="stat-value">{{ authStore.roles.join(', ') || '-' }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <div class="stat-label">权限数</div>
          <div class="stat-value">{{ authStore.permissions.length }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="welcome" shadow="never">
      <h3>欢迎使用 Polaris Admin</h3>
      <p>本示例演示前后端分离下的登录鉴权、RBAC 权限控制与用户 CRUD。</p>
      <ul>
        <li>后端：FastAPI + SQLAlchemy + JWT + 分层架构</li>
        <li>前端：Vue3 + Pinia + Vue Router + Element Plus</li>
        <li>权限码示例：user:list / user:create / role:update</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.stat-label {
  color: #6b7280;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 22px;
  font-weight: 600;
}

.welcome {
  margin-top: 16px;
}

.welcome h3 {
  margin-top: 0;
}

.welcome ul {
  margin: 0;
  padding-left: 18px;
  color: #4b5563;
  line-height: 1.8;
}
</style>
