## Data from production
```
ids = [11180, 7173, 4548, 17519, 14623, 8011, 13976, 17177, 18306, 9694, 10591, 10928, 1779, 7796, 10404, 6519, 11972, 20978, 20827, 16715, 21060]
profiles = []
cps = CampaignProfile.where(id: ids)
cps.each do |cp|
  stories = cp.campaign_posts.where(media_type: "Story").where.not(insights_screenshot: nil)
  stories.each do |s|
    story_stat = s.campaign_post_stats.last #:reach, :swipe_ups_count, :tap_count
    insta_details = cp.insta_user.insta_user_bios.where('created_at >=?',story_stat.created_at).first
    # :followers, :avg_engagement_month, :ffratio, :total_likes, :total_comments
    profiles << ([cp].pluck(:id) + [story_stat].pluck(:reach, :swipe_ups_count, :tap_count) + [insta_details].pluck(:followers, :avg_engagement_month, :ffratio, :total_likes, :total_comments)).flatten!
  end
end
```
```
cps = CampaignPost.where("media_type = 'Story' and verified = 'approved'")
cps.count
data = []
cps.each do |c|
  if !c.campaign_post_stats.empty?
    stat = c.campaign_post_stats.last
    if !c.campaign_profile.nil?
      insta = c.campaign_profile.insta_user
      if !insta.nil?
        bios = InstaUserBio.where('insta_user_id = ? and created_at < ?',insta.id,c.created_at)
        if !bios.empty?
          bios = bios.last
          data << ([bios].pluck(:followers, :avg_engagement_month) + [stat].pluck(:reach,:swipe_ups_count)).flatten!
        end
      end
    end
  end
end
data.each do |d|
  d.each_with_index do |e,i|
    if e == nil
      d[i] = 0
    end
  end
end
```
