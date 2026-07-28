<template>
  <div class="user-page">
    <el-card shadow="never">
      <div class="toolbar">
        <el-form :inline="true" :model="query">
          <el-form-item label="关键词">
            <el-input v-model="query.keyword" placeholder="用户名/邮箱/姓名" clearable @keyup.enter="handleSearch" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="query.is_active" clearable placeholder="全部" style="width: 120px">
              <el-option label="启用" :value="true" />
              <el-option label="禁用" :value="false" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
        <el-button v-permission="'user:create'" type="primary" @click="openCreate">新建用户</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="full_name" label="姓名" min-width="120" />
        <el-table-column label="角色" min-width="160">
          <template #default="{ row }">
            <el-tag v-for="role in row.roles" :key="role.id" size="small" class="role-tag">
              {{ role.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="'user:update'" type="primary" link @click="openEdit(row)">编辑</el-button>
            <el-button
              v-permission="'user:delete'"
              type="danger"
              link
              :disabled="row.is_superuser"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pager">
        <el-pagination
          v-model:current-page="query.page"
          v-model:page-size="query.page_size"
          background
          layout="total, sizes, prev, pager, next"
          :total="total"
          :page-sizes="[10, 20, 50]"
          @current-change="fetchList"
          @size-change="handleSearch"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '新建用户'" width="520px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item v-if="!isEdit" label="用户名" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="form.full_name" />
        </el-form-item>
        <el-form-item :label="isEdit ? '新密码' : '密码'" :prop="isEdit ? undefined : 'password'">
          <el-input v-model="form.password" type="password" show-password :placeholder="isEdit ? '不修改请留空' : ''" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="form.is_active" />
        </el-form-item>
        <el-form-item label="角色" prop="role_ids">
          <el-select v-model="form.role_ids" multiple placeholder="请选择角色" style="width: 100%">
            <el-option v-for="role in roleOptions" :key="role.id" :label="role.name" :value="role.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage, ElMessageBox } from 'element-plus'
import { createUserApi, deleteUserApi, listUsersApi, updateUserApi } from '@/api/user'
import { listRolesApi } from '@/api/role'
import type { RoleItem, UserItem } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const tableData = ref<UserItem[]>([])
const total = ref(0)
const roleOptions = ref<RoleItem[]>([])
const formRef = ref<FormInstance>()

const query = reactive({
  keyword: '',
  is_active: null as boolean | null,
  page: 1,
  page_size: 10,
})

const form = reactive({
  username: '',
  email: '',
  full_name: '',
  password: '',
  is_active: true,
  role_ids: [] as number[],
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function fetchList() {
  loading.value = true
  try {
    const data = await listUsersApi({
      keyword: query.keyword || undefined,
      is_active: query.is_active ?? undefined,
      page: query.page,
      page_size: query.page_size,
    })
    tableData.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function fetchRoles() {
  roleOptions.value = await listRolesApi()
}

function handleSearch() {
  query.page = 1
  fetchList()
}

function handleReset() {
  query.keyword = ''
  query.is_active = null
  handleSearch()
}

function resetForm() {
  form.username = ''
  form.email = ''
  form.full_name = ''
  form.password = ''
  form.is_active = true
  form.role_ids = []
}

function openCreate() {
  isEdit.value = false
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEdit(row: UserItem) {
  isEdit.value = true
  editingId.value = row.id
  form.username = row.username
  form.email = row.email
  form.full_name = row.full_name || ''
  form.password = ''
  form.is_active = row.is_active
  form.role_ids = row.roles.map((item) => item.id)
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid && !isEdit.value) return
  if (isEdit.value) {
    const emailValid = await formRef.value?.validateField('email').catch(() => false)
    if (!emailValid) return
  }

  submitting.value = true
  try {
    if (isEdit.value && editingId.value != null) {
      await updateUserApi(editingId.value, {
        email: form.email,
        full_name: form.full_name || undefined,
        is_active: form.is_active,
        password: form.password || undefined,
        role_ids: form.role_ids,
      })
      ElMessage.success('用户已更新')
    } else {
      await createUserApi({
        username: form.username,
        email: form.email,
        password: form.password,
        full_name: form.full_name || undefined,
        is_active: form.is_active,
        role_ids: form.role_ids,
      })
      ElMessage.success('用户已创建')
    }
    dialogVisible.value = false
    await fetchList()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: UserItem) {
  await ElMessageBox.confirm(`确认删除用户「${row.username}」？`, '删除确认', { type: 'warning' })
  await deleteUserApi(row.id)
  ElMessage.success('用户已删除')
  await fetchList()
}

onMounted(async () => {
  await Promise.all([fetchList(), fetchRoles()])
})
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.role-tag {
  margin-right: 4px;
}

.pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
