<template>
  <div class="flex justify-center"><p class="font-bold text-[30px]">用户列表</p></div>
  <div class="p-[32px] mt-[32px] bg-[#F1E9F8] border rounded-xl w-full font-semibold text-[20px] text-[#EBEEF5]">
    <el-button type="primary" @click="addUserDialogVisible = true">添加用户</el-button>

    <div class="flex mt-[16px] bg-[#D8BFD8] text-[#1F75CB]">
      <span class="flex justify-center w-[80px] border">id</span>
      <span class="flex justify-center w-[150px] border">name</span>
      <span class="flex justify-center w-[100px] border">gender</span>
      <span class="flex justify-center w-[80px] border">edit</span>
    </div>
    <div v-for="(user, index) in users" :key="user.id" class="flex mt-[16px] bg-[#D8BFD8] text-[#1F75CB]">
      <span class="flex justify-center w-[80px] border">{{ user.id }}</span>
      <span class="flex justify-center w-[150px] border whitespace-nowrap overflow-hidden"><p>{{user.username }}</p></span>
      <span class="flex justify-center w-[100px] border">{{ user.gender }}</span>
      <a @click="editUser(index)" class="cursor-pointer hover:bg-[#6A0572] hover:text-[#FFFFFF]"><span
          class="flex justify-center w-[80px] border">edit</span></a>
    </div>

    <el-pagination background
                   v-model:current-page="currentPage"
                   :default-current-page=1
                   :total="Number(totalUsers)"
                   :page-size="5"
                   layout="prev, pager, next"
                   @update:current-page="nextPage"
                   class="mt-[52px]"
    />


    <el-dialog v-model="addUserDialogVisible" title="添加用户" width="30%" class="dialogWidth"
               style="border-radius: 0.5rem;" left>
      <div class="flex">
        <label class="flex items-center justify-center w-[100px] mr-[16px] text-[16px]"><p>用户名 :</p></label>
        <div class="w-[230px]">
          <el-input
              v-model="userName"
              class="w-[40px]"
              maxlength="10"
              placeholder="请输入用户名"></el-input>
        </div>
      </div>
      <div class="flex mt-[32px]">
        <label class="flex items-center justify-center w-[100px] mr-[16px] text-[16px]"><p>性别 :</p></label>
        <el-select v-model="gender" placeholder="选择">
          <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </div>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="addUserDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitTheForm">
          确认
        </el-button>
      </span>
      </template>
    </el-dialog>

    <el-dialog v-model="editUserDialogVisible" title="编辑用户" width="30%" class="dialogWidth"
               style="border-radius: 0.5rem;" left>
      <div class="flex">
        <label class="flex items-center justify-center w-[100px] mr-[16px] text-[16px]"><p>用户名 :</p></label>
        <div class="w-[230px]">
          <el-input
              v-model="placeholderName"
              class="w-[40px]"
              maxlength="10"
              :placeholder="placeholderName"></el-input>
        </div>
      </div>
      <div class="flex mt-[32px]">
        <label class="flex items-center justify-center w-[100px] mr-[16px] text-[16px]"><p>性别 :</p></label>
        <el-select v-model="placeholderGender" placeholder="选择">
          <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </div>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="editUserDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitTheEditForm">
          确认
        </el-button>
      </span>
      </template>
    </el-dialog>


  </div>
</template>

<script setup>
import {ElMessage} from "element-plus"
import {ref, onMounted} from 'vue'
import {useCookies} from "vue3-cookies"
import axios from 'axios';

let users = ref([])
const totalUsers = ref()
let currentPage = ref(1)
const {cookies} = useCookies()

onMounted(async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/users?page=${currentPage.value}`);
    const data = response.data;

    users.value = data.users;
    totalUsers.value = data.total_users;
  } catch (error) {
    console.error('发生错误:', error);
  }
});

let addUserDialogVisible = ref(false)
let editUserDialogVisible = ref(false)
let userName = ref('')
let gender = ref('male')
const options = ref([{value: 'male', label: '男'}, {value: 'female', label: '女'}])

// 分页
const nextPage = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/users?page=${currentPage.value}`);
    const data = response.data;

    users.value = data.users;
    totalUsers.value = data.total_users;
  } catch (error) {
    console.error('发生错误:', error);
  }
}

const submitTheForm = () => {
  if (!userName.value) {
    ElMessage({message: "请您填写姓名", type: "warning"})
    return
  }
  if (userName.value.trim() == '') {
    ElMessage({message: "输入不合法", type: "warning"})
    userName.value = ''
    return
  }
  addUserDialogVisible.value = false
  addUser().catch(err => {
    ElMessage({
      message: err.message,
      type: 'warning'
    })
  })
}

const addUser = async () => {
  const addUserEndpoint = 'http://127.0.0.1:5000/api/users';

  try {
    const response = await axios.post(addUserEndpoint, {
      username: userName.value,
      gender: gender.value,
    }, {
      headers: {'Content-Type': 'application/json'},
    });

    ElMessage({ message: "添加成功", type: "success" });
    setTimeout(() => {
      window.location.href = "/";
    }, 500);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message);
    } else if (error.request) {
      throw new Error("未收到响应");
    } else {
      throw new Error("请求设置错误");
    }
  }
};

let placeholderName = ref('')
let placeholderGender = ref('')
var userId = null
var userIndex = null

// 点击编辑
const editUser = (index) => {
  placeholderName.value = users.value[index].username
  placeholderGender.value = users.value[index].gender
  userId = users.value[index].id
  userIndex = index
  editUserDialogVisible.value = true
}

const submitTheEditForm = () => {
  if (!placeholderName.value) {
    ElMessage({message: "请您填写姓名", type: "warning"})
    return
  }
  if (placeholderName.value.trim() == '') {
    ElMessage({message: "输入不合法", type: "warning"})
    userName.value = ''
    return
  }
  editUserDialogVisible.value = false
  updateUser().then(data => {
    users.value[userIndex].username = data.user.username
    users.value[userIndex].gender = data.user.gender
  }).catch(err => {
    ElMessage({
      message: err.message,
      type: 'warning'
    })
  })
}

// 更新用户api
const updateUser = async () => {
  const updateUserEndpoint = `http://127.0.0.1:5000/api/users/${userId}`;

  try {
    const response = await axios.put(updateUserEndpoint, {
      username: placeholderName.value,
      gender: placeholderGender.value,
    }, {
      headers: {'Content-Type': 'application/json'},
    });

    ElMessage({ message: "用户更新成功", type: "success" });
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.message);
    } else if (error.request) {
      throw new Error("未收到响应");
    } else {
      throw new Error("请求设置错误");
    }
  }
};
</script>
<style>
.dialogWidth {
  width: 30%;
}

@media (max-width: 640px) {
  .dialogWidth {
    width: 80%;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .dialogWidth {
    width: 50%;
  }
}

@media (min-width: 1025px) {
  .dialogWidth {
    width: 30%;
  }
}
</style>