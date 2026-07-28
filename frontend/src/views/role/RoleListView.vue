<template>
  <div class="role-page">
    <el-card shadow="never">
      <div class="toolbar">
        <div class="title">角色列表</div>
        <el-button v-permission="'role:create'" type="primary" @click="openCreate">新建角色</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="code" label="编码" min-width="120" />
        <el-table-column prop="name" label="名称" min-width="140" />
        <el-table-column prop="description" label="描述" min-width="180" />
        <el-table-column label="权限" min-width="260">
          <template #default="{ row }">
            <el-tag
              v-for="permission in row.permissions"
              :key="permission.id"
              size="small"
              class="perm-tag"
            >
              {{ permission.code }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="'role:update'" type="primary" link @click="openEdit(row)">编辑</el-button>
            <el-button
              v-permission="'role:delete'"
              type="danger"
              link
              :disabled="row.code === 'admin'"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑角色' : '新建角色'" width="560px" destroy-on-close>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item v-if="!isEdit" label="编码" prop="code">
          <el-input v-model="form.code" placeholder="例如 editor" />
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="权限" prop="permission_ids">
          <el-checkbox-group v-model="form.permission_ids">
            <el-checkbox
              v-for="item in permissionOptions"
              :key="item.id"
              :label="item.id"
              :value="item.id"
            >
              {{ item.code }}（{{ item.name }}）
            </el-checkbox>
          </el-checkbox-group>
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
import {
  createRoleApi,
  deleteRoleApi,
  listPermissionsApi,
  listRolesApi,
  updateRoleApi,
} from '@/api/role'
import type { PermissionItem, RoleItem } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const tableData = ref<RoleItem[]>([])
const permissionOptions = ref<PermissionItem[]>([])
const formRef = ref<FormInstance>()

const form = reactive({
  code: '',
  name: '',
  description: '',
  permission_ids: [] as number[],
})

const rules: FormRules = {
  code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
}

async function fetchList() {
  loading.value = true
  try {
    tableData.value = await listRolesApi()
  } finally {
    loading.value = false
  }
}

async function fetchPermissions() {
  permissionOptions.value = await listPermissionsApi()
}

function resetForm() {
  form.code = ''
  form.name = ''
  form.description = ''
  form.permission_ids = []
}

function openCreate() {
  isEdit.value = false
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEdit(row: RoleItem) {
  isEdit.value = true
  editingId.value = row.id
  form.code = row.code
  form.name = row.name
  form.description = row.description || ''
  form.permission_ids = row.permissions.map((item) => item.id)
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid && !isEdit.value) return
  if (isEdit.value) {
    const nameValid = await formRef.value?.validateField('name').catch(() => false)
    if (!nameValid) return
  }

  submitting.value = true
  try {
    if (isEdit.value && editingId.value != null) {
      await updateRoleApi(editingId.value, {
        name: form.name,
        description: form.description || undefined,
        permission_ids: form.permission_ids,
      })
      ElMessage.success('角色已更新')
    } else {
      await createRoleApi({
        code: form.code,
        name: form.name,
        description: form.description || undefined,
        permission_ids: form.permission_ids,
      })
      ElMessage.success('角色已创建')
    }
    dialogVisible.value = false
    await fetchList()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: RoleItem) {
  await ElMessageBox.confirm(`确认删除角色「${row.name}」？`, '删除确认', { type: 'warning' })
  await deleteRoleApi(row.id)
  ElMessage.success('角色已删除')
  await fetchList()
}

onMounted(async () => {
  await Promise.all([fetchList(), fetchPermissions()])
})
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.perm-tag {
  margin: 0 4px 4px 0;
}

:deep(.el-checkbox) {
  width: 100%;
  margin-right: 0;
  margin-bottom: 6px;
}
</style>
