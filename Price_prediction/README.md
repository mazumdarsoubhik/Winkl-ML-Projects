# Data Gathering
> Open SSH (rails production) on PC and run the following </br>
> Copy the array printed and store it in txt </br>
> Parse txt to make csv </br>
> Columns = "campaign_profile_id", "campaign_post_format_id", "insta_user_id", "followers", "avg_engangement", "price"
```ruby
cppf = CampaignProfilePostFormat.where.not(price:0).offset(0).limit(20000)
cppf.count
details = []
cppf.each do |c|
  cp = c.campaign_profile
  if !cp.nil?
    iu = cp.insta_user
    if !iu.nil?
      ia = iu.instagram_account
      if !ia.nil?
        details << ([cp].pluck(:id) + [c].pluck(:campaign_post_format_id) + [ia].pluck(:insta_user_id,:followers,:avg_engagement) + [c].pluck(:price)).flatten!
      end
    end
  end
end
details.each do |d|
  d.each_with_index do |e,i|
    if e == nil
      d[i] = 0
    end
  end
end
```
