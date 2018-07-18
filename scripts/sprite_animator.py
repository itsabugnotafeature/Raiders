from scripts import animations


class SpriteAnimator:

    def __init__(self, sprite):

        self.sprite = sprite

    def use(self, ability, animator):
        try:
            animator.set_animation(self.sprite, ability.animation)
        except AttributeError:
            print("Failed to find animation for {}'s [{}] ability .".format(self.sprite.name, ability.name))
            print("Reverting to default animation,")
            animator.set_animation(self.sprite, animations.attack())
