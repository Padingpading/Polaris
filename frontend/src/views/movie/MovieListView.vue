<template>
  <div class="movie-page">
    <el-card shadow="never">
      <div class="toolbar">
        <el-form :inline="true" :model="query">
          <el-form-item label="关键词">
            <el-input
              v-model="query.keyword"
              placeholder="片名/导演/简介"
              clearable
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="类型">
            <el-input v-model="query.genre" placeholder="如 科幻" clearable style="width: 120px" />
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="query.is_active" clearable placeholder="全部" style="width: 120px">
              <el-option label="上架" :value="true" />
              <el-option label="下架" :value="false" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
        <el-button v-permission="'movie:create'" type="primary" @click="openCreate">新建电影</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="片名" min-width="160" />
        <el-table-column prop="director" label="导演" min-width="120" />
        <el-table-column prop="genre" label="类型" width="100" />
        <el-table-column prop="release_year" label="年份" width="90" />
        <el-table-column prop="duration_minutes" label="时长(分)" width="100" />
        <el-table-column prop="rating" label="评分" width="80" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '上架' : '下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button v-permission="'movie:update'" type="primary" link @click="openEdit(row)">
              编辑
            </el-button>
            <el-button v-permission="'movie:delete'" type="danger" link @click="handleDelete(row)">
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

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑电影' : '新建电影'"
      width="560px"
      destroy-on-close
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="片名" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="导演" prop="director">
          <el-input v-model="form.director" />
        </el-form-item>
        <el-form-item label="类型" prop="genre">
          <el-input v-model="form.genre" placeholder="如 动作 / 科幻 / 喜剧" />
        </el-form-item>
        <el-form-item label="年份" prop="release_year">
          <el-input-number v-model="form.release_year" :min="1888" :max="2100" controls-position="right" />
        </el-form-item>
        <el-form-item label="时长(分)" prop="duration_minutes">
          <el-input-number
            v-model="form.duration_minutes"
            :min="1"
            :max="1000"
            controls-position="right"
          />
        </el-form-item>
        <el-form-item label="评分" prop="rating">
          <el-input-number
            v-model="form.rating"
            :min="0"
            :max="10"
            :step="0.1"
            :precision="1"
            controls-position="right"
          />
        </el-form-item>
        <el-form-item label="简介" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="上架">
          <el-switch v-model="form.is_active" />
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
  createMovieApi,
  deleteMovieApi,
  listMoviesApi,
  updateMovieApi,
} from '@/api/movie'
import type { MovieItem } from '@/types'

const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const tableData = ref<MovieItem[]>([])
const total = ref(0)
const formRef = ref<FormInstance>()

const query = reactive({
  keyword: '',
  genre: '',
  is_active: null as boolean | null,
  page: 1,
  page_size: 10,
})

const form = reactive({
  title: '',
  director: '',
  genre: '',
  release_year: undefined as number | undefined,
  duration_minutes: undefined as number | undefined,
  rating: undefined as number | undefined,
  description: '',
  is_active: true,
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入片名', trigger: 'blur' }],
}

async function fetchList() {
  loading.value = true
  try {
    const data = await listMoviesApi({
      keyword: query.keyword || undefined,
      genre: query.genre || undefined,
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

function handleSearch() {
  query.page = 1
  fetchList()
}

function handleReset() {
  query.keyword = ''
  query.genre = ''
  query.is_active = null
  handleSearch()
}

function resetForm() {
  form.title = ''
  form.director = ''
  form.genre = ''
  form.release_year = undefined
  form.duration_minutes = undefined
  form.rating = undefined
  form.description = ''
  form.is_active = true
}

function openCreate() {
  isEdit.value = false
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEdit(row: MovieItem) {
  isEdit.value = true
  editingId.value = row.id
  form.title = row.title
  form.director = row.director || ''
  form.genre = row.genre || ''
  form.release_year = row.release_year ?? undefined
  form.duration_minutes = row.duration_minutes ?? undefined
  form.rating = row.rating != null ? Number(row.rating) : undefined
  form.description = row.description || ''
  form.is_active = row.is_active
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  const payload = {
    title: form.title,
    director: form.director || undefined,
    genre: form.genre || undefined,
    release_year: form.release_year,
    duration_minutes: form.duration_minutes,
    rating: form.rating,
    description: form.description || undefined,
    is_active: form.is_active,
  }

  submitting.value = true
  try {
    if (isEdit.value && editingId.value != null) {
      await updateMovieApi(editingId.value, payload)
      ElMessage.success('电影已更新')
    } else {
      await createMovieApi(payload)
      ElMessage.success('电影已创建')
    }
    dialogVisible.value = false
    await fetchList()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: MovieItem) {
  await ElMessageBox.confirm(`确认删除电影「${row.title}」？`, '删除确认', { type: 'warning' })
  await deleteMovieApi(row.id)
  ElMessage.success('电影已删除')
  await fetchList()
}

onMounted(fetchList)
</script>

<style scoped>
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 8px;
}

.pager {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}
</style>
