def sum3(nums):
    n = len(nums)
    if n < 3:
        return []
    nums.sort()
    res = []
    i = 0
    while i < n - 2 and nums[i] < 0:
        l = i + 1
        r = n - 1
        if i > 0 and nums[i] == nums[i-1]:
            i += 1
            continue
        
        while l < r:
            if nums[l] + nums[r] + nums[i] == 0:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l+1]:
                    l += 1
                l += 1
                while l < r and nums[r] == nums[r-1]:
                    r -= 1
                r -= 1
            elif nums[l] + nums[r] + nums[i] < 0:
                l += 1
            else:
                r -= 1
        i += 1
    return res


if __name__ == '__main__':
    nums = [1,2,5,9,-1,-2,-4,0]
    res = sum3(nums)
    print(res)
